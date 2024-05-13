import argparse
import re

def is_match(pattern, string):
    match = re.match(pattern, string)
    return match is not None and match.end() == len(string)


class MOPFile :
    def __init__(self, file):
        self.file = file
        self.specname = ""
        self.params = []
        self.includes = []
        self.events = []
        if self.check_file():
            self.parse_file()
            self.header_fileout = f"{self.specname}_dispatcher.h"
            self.source_fileout = f"{self.specname}_dispatcher.cpp"
            self.dispatcher_class_name = f"{self.specname}_dispatcher"
            self.monitor_class_name = f"{self.specname}_Monitor"
            self.num_params = len(self.params)
            self.bot_string = ('nullptr, ' * self.num_params)[:-2]
            self.set_theta_t_type()
        else:
            print(f"File: {file} not formatted correctly")
            exit(1)

    def check_file(self):
        try:
            with open(self.file, 'r') as f:
                lines = f.readlines()

            in_header = False
            for line in lines:
                line = line.strip()
                if in_header:
                    if len(line) == 0 or line.startswith("#include"):
                        continue
                    if not is_match(r'.*\(.*\).*', line):
                        return False
                    in_header = False

            return True
        except FileNotFoundError as e:
            print(f"File {self.file} not found")
            exit(1)

    def parse_file(self):
        try:
            with open(self.file, 'r') as f:
                lines = f.readlines()

            in_header = True
            for line in lines:
                line = line.strip()
                if in_header:
                    if line.startswith("#include"):
                        self.includes.append(line)
                    elif len(line) > 0:
                        # parse spec name and parameters
                        in_header = False
                        self.specname = line[:line.find('(')].strip()
                        param_string = line[line.find('(')+1:line.find(')')]
                        parts = param_string.split(',')
                        for part in parts:
                            self.params.append(part.strip())
                else:
                    if line.startswith('event'):
                        parts = line.split()
                        event_name = parts[1]
                        event_params = ""

                        param_string = line[line.find('(')+1:line.find(')')].strip()
                        if not param_string.startswith('void '):
                            event_params = param_string
                        self.events.append((event_name, event_params))
                    
        except Exception as e:
            print("Exception occured: ", e)
    
    def set_theta_t_type(self):
        theta_t_type = "std::tuple<"
        for param in self.params:
            param_type = param.split()[0]
            assert '&' not in param_type
            theta_t_type += param_type + '*, '
        theta_t_type = theta_t_type[:-2]
        theta_t_type += ">"
        self.theta_t_type = theta_t_type
        

def generate_header(mop : MOPFile, file_out):
    file_out.write('// This is a generated dispatcher for non-parametric monitoring\n\n')
    file_out.write('#pragma once\n\n')
    file_out.write(f'#include "{mop.specname}_monitor.h"\n')
    for include in mop.includes:
        file_out.write(f'{include}\n')
    file_out.write('\n')
    file_out.write(f'class {mop.dispatcher_class_name}\n')
    file_out.write('{\n')
    file_out.write('private:\n')
    file_out.write(f'\t{mop.monitor_class_name} monitor {{}};\n\n')
    file_out.write('public:\n')
    for event_name, event_params in mop.events:
        file_out.write(f'\tvoid receive_{event_name}({event_params});\n')
    file_out.write('};\n')

def generate_source(mop : MOPFile, file_out):
    file_out.write('// This is a generated dispatcher for non-parametric monitoring\n\n')
    file_out.write(f'#include "{mop.header_fileout}"\n\n')
    for event in mop.events:
        event_name = event[0]
        event_params = event[1]
        file_out.write(f'void {mop.dispatcher_class_name}::receive_{event_name}({event_params})\n')
        file_out.write('{\n')
        file_out.write(f'\tmonitor.__RVC_{mop.specname}_{event_name}();\n')
        file_out.write('}\n\n')

def generate_header_parametric(mop : MOPFile, file_out):
    file_out.write('// This is a generated dispatcher for parametric monitoring\n\n')
    file_out.write('#pragma once\n\n')
    file_out.write(f'#include <tuple>\n')
    file_out.write(f'#include <unordered_map>\n')
    file_out.write(f'#include <unordered_set>\n')
    file_out.write(f'#include "{mop.specname}_monitor.h"\n')
    for include in mop.includes:
        file_out.write(f'{include}\n')
    file_out.write('\n')
    file_out.write('''\
template<typename T>
std::size_t hash_pointer(const T* ptr) {
    return reinterpret_cast<std::size_t>(ptr);
}\n''')
    file_out.write('struct tuple_hash {\n')
    write_out(file_out, get_tuple_hash_lines(mop), '\t')
    file_out.write('}\n')
    file_out.write(f'class {mop.dispatcher_class_name}\n')
    file_out.write('{\n')
    file_out.write(f'using theta_t = {mop.theta_t_type}\n')
    file_out.write('using Theta_t = std::unordered_set<theta_t, tuple_hash>\n\n')
    file_out.write('private:\n')
    write_out(file_out, get_private_lines(mop), '\t')
    file_out.write('public:\n')
    write_out(file_out, get_public_lines(mop), '\t')
    file_out.write('};\n')


def generate_source_parametric(mop : MOPFile, file_out):
    file_out.write('// This is a generated dispatcher for parametric monitoring\n\n')
    file_out.write(f'#include "{mop.header_fileout}"\n\n')
    
    for e_idx, (event_name, event_params) in enumerate(mop.events):
        file_out.write(f'void {mop.dispatcher_class_name}::receive_{event_name}({event_params}) {{\n')
        theta_string = get_theta_string(mop, event_params)
        file_out.write(f'\ttheta_t theta = {{{theta_string}}};\n')
        file_out.write(f'\treceive({e_idx}, theta);\n')
        file_out.write('}\n\n')
    
def get_theta_string(mop : MOPFile, event_params : str):
    event_params_map = {}
    event_params = event_params.strip()
    if len(event_params) != 0:
        for event_param in event_params.split(','):
            event_param = event_param.strip()
            event_param = event_param.replace('&', '')
            assert len(event_param.split()) == 2
            event_param_type = event_param.split()[0]
            event_param_var = event_param.split()[1]
            event_params_map[event_param_type] = event_param_var
    
    parts = []
    for param in mop.params:
        param_type = param.split()[0]
        if param_type in event_params_map:
            parts.append(f'&{event_params_map[param_type]}')
        else:
            parts.append('nullptr')
            
    return ', '.join(parts)

def write_out(file_out, lines, prefix=""):
    for line in lines:
        file_out.write(prefix + line + '\n')

def get_tuple_hash_lines(mop : MOPFile):
    lines = [
        f'using theta_t = {mop.theta_t_type}',
        'template <std::size_t N>',
        'std::size_t operator()(const theta_t& tuple) const {',
        '\tstd::size_t seed = 0;',
        '\thash_combine(seed, std::get<N>(tuple));',
        '\treturn seed;',
        '}',
        '',
        'std::size_t operator()(const std::tuple<Car*, Person*, OneLaneBridge*>& tuple) const {',
        '\treturn hash_combine<0>(tuple);',
        '}',
        '',
        'template <std::size_t N>',
        f'std::size_t hash_combine(const {mop.theta_t_type}& tuple) const {{',
            '\tstd::size_t seed = 0;',
            '\tseed ^= hash_pointer(std::get<N>(tuple)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);',
            '\treturn seed;',
        '}',
        '',
        'template <std::size_t N, std::size_t M, typename... Ts>',
        f'std::size_t hash_combine(const {mop.theta_t_type}& tuple) const {{',
            '\tstd::size_t seed = hash_combine<N>(tuple);',
            '\tseed = hash_combine<M, Ts...>(tuple);',
            '\treturn seed;',
        '}',
    ]
    return lines

def get_private_lines(mop : MOPFile):
    lines = [
        f'std::vector<{mop.monitor_class_name}*> monitors {{}};',
        'Theta_t Theta {};',
        f'std::unordered_map<theta_t, {mop.monitor_class_name}*, tuple_hash> Delta {{}};',
        '',
    ]
    lines.extend(get_compatible_lines(mop))
    lines.extend(get_computeCombine_lines(mop))
    lines.extend(get_computeCombine2_lines(mop))
    lines.extend(get_updateTheta_lines(mop))
    lines.extend(get_computeSet_lines(mop))
    lines.extend(get_max_lines(mop))
    lines.extend(get_less_informative_lines(mop))
    lines.extend(get_receive_lines(mop))
    lines.extend(get_receive_lines(mop))
    lines.extend(get_monitor_receive_lines(mop))
    
    return lines

def get_lines_for_method(header, body):
    lines = [header]
    for line in body:
        lines.append('\t' + line)
    lines.append('}')
    lines.append('')
    return lines

def get_compatible_lines(mop : MOPFile):
    header = 'bool compatible(const theta_t& theta1, const theta_t& theta2) {'
    body = []
    for theta_i in [1, 2]:
        for p_idx in range(mop.num_params):
            body.append(f'auto* v{p_idx}_{theta_i} = std::get<{p_idx}>(theta{theta_i});')
    for p_idx in range(mop.num_params):
        body.append(f'if (v{p_idx}_1 != v{p_idx}_2 && v{p_idx}_1 != nullptr && v{p_idx}_2 != nullptr) {{')
        body.append('\treturn false;')
        body.append('}')
    body.append('return true;')
    return get_lines_for_method(header, body)

def get_computeCombine_lines(mop : MOPFile):
    header = 'theta_t computeCombine(const theta_t& theta1, const theta_t& theta2) {'
    body = []
    for p_idx in range(mop.num_params):
        body.append(f'auto* v{p_idx} = std::get<{p_idx}>(theta1);')
    
    for p_idx in range(mop.num_params):
        body.append(f'if (std::get<{p_idx}>(theta2) != nullptr) {{')
        body.append(f'\tv{p_idx} = std::get<{p_idx}>(theta2);')
        body.append('}')

    ret_string = 'return {'
    for p_idx in range(mop.num_params):
        ret_string += f'v{p_idx}, '
        ret_string = ret_string[:-2]
    ret_string += '};'
    body.append(ret_string)
    
    return get_lines_for_method(header, body)

def get_computeCombine2_lines(mop : MOPFile):
    header = 'Theta_t computeCombine(const theta_t& theta) {'
    body = """Theta_t all_combine {};
for (const theta_t& theta_prime : Theta) {
    if (compatible(theta, theta_prime)) {
        theta_t combine = computeCombine(theta, theta_prime);
        all_combine.insert(combine);
    }
}
return all_combine;""".split('\n')
    return get_lines_for_method(header, body)

def get_updateTheta_lines(mop : MOPFile):
    header = 'void updateTheta(const theta_t& theta) {'
    body = """Theta_t combine_theta = computeCombine(theta);
for (const theta_t& theta_prime : combine_theta) {
    Theta.insert(theta_prime);
}""".split('\n')
    return get_lines_for_method(header, body)

def get_computeSet_lines(mop : MOPFile):
    header = 'Theta_t computeSet(const theta_t& theta) {'
    body = """Theta_t set {};
for (const theta_t& theta_prime : Theta) {
    if (less_informative(theta_prime, theta)) {
        set.insert(theta_prime);
    }
}
return set;""".split('\n')
    return get_lines_for_method(header, body)

def get_max_lines(mop : MOPFile):
    header = 'theta_t max(const Theta_t& Theta) {'
    body = """theta_t curr_max = {BOT};
for (const theta_t& theta : Theta) {
    if (less_informative(curr_max, theta)) {
        curr_max = theta;
    }
}
return curr_max;""".split('\n')
    body[0] = body[0].replace('BOT', mop.bot_string)
    return get_lines_for_method(header, body)

def get_less_informative_lines(mop : MOPFile):
    header = 'bool less_informative(const theta_t& theta1, const theta_t& theta2) {'
    body = []
    for theta_i in [1, 2]:
        for p_idx in range(mop.num_params):
            body.append(f'auto* v{p_idx}_{theta_i} = std::get<{p_idx}>(theta{theta_i});')

    for p_idx in range(mop.num_params):
        body.append(f'if (v{p_idx}_1 != nullptr && v{p_idx}_1 != v{p_idx}_2) {{')
        body.append('\treturn false;')
        body.append('}')
    body.append('return true;')
    
    return get_lines_for_method(header, body)

def get_receive_lines(mop : MOPFile):
    header = 'void receive(int event_id, theta_t& theta) {'
    body = f"""Theta_t domain = computeCombine(theta);
for (const theta_t& theta_prime : domain) {{
    if (Theta.count(theta_prime) > 0) {{
        // if theta' is in Theta, max (theta']_Theta = theta' and monitor already is created
        {mop.monitor_class_name}& m = *Delta[theta_prime];
        monitor_receive(m, event_id);
    }} else {{
        Theta_t set = computeSet(theta_prime);
        theta_t max_theta = max(set);
        {mop.monitor_class_name}* m = new {mop.monitor_class_name}(*Delta[max_theta]);
        monitors.push_back(m);
        Delta[theta_prime] = m;
        monitor_receive(*m, event_id);
    }}
}}
updateTheta(theta);""".split('\n')
    return get_lines_for_method(header, body)

def get_monitor_receive_lines(mop : MOPFile):
    header = f'void monitor_receive({mop.monitor_class_name}& monitor, int event_id) {{'
    body = ['switch (event_id) {']
    for e_id in range(len(mop.events)):
        body.append(f'\tcase {e_id}:')
        body.append(f'\t\tmonitor.__RVC_{mop.monitor_class_name}_{mop.events[e_id][0]}();')
        body.append('\t\tbreak;')
    body.append('}')
    return get_lines_for_method(header, body)

def get_public_lines(mop : MOPFile):
    lines = get_dispatcher_lines(mop)
    lines.extend(get_receive_functions_lines(mop))
    
    return lines

def get_dispatcher_lines(mop : MOPFile):
    header = f'{mop.dispatcher_class_name} () {{'
    body = f"""Spec1_Monitor* m = new Spec1_Monitor();
monitors.push_back(m);
theta_t bot = {{{mop.bot_string}}};
Delta[bot] = m;
Theta.insert(bot);""".split('\n')
    return get_lines_for_method(header, body)

def get_receive_functions_lines(mop : MOPFile):
    lines = []
    for event_name, event_params in mop.events:
        lines.append(f'void receive_{event_name}({event_params});')
    return lines


def print_mop(mop : MOPFile):
    print(mop.file)
    print(mop.specname)
    print(mop.params)
    print(mop.includes)
    print(mop.events)

def main():
    parser = argparse.ArgumentParser(description='Generate dispatcher from .mop file.')

    parser.add_argument('filename', type=str, help='Input file name')
    parser.add_argument('-p', '--parametric', action='store_true', help='Use parametric monitoring')

    args = parser.parse_args()

    # Access the parsed arguments
    filename = args.filename
    do_parametric = args.parametric

    mop = MOPFile(filename)
    print_mop(mop)

    if do_parametric:
        try:
            with open(mop.source_fileout, 'w') as f:
                generate_source_parametric(mop, f)
            with open(mop.header_fileout, 'w') as f:
                generate_header_parametric(mop, f)
        except Exception as e:
            print("Something went wrong generating parametric dispatcher")
            raise(e)
            exit(1)
    else:
        try:
            with open(mop.source_fileout, 'w') as f:
                generate_source(mop, f)
            with open(mop.header_fileout, 'w') as f:
                generate_header(mop, f)
        except Exception as e:
            print("Something went wrong generating dispatcher")
            exit(1)


if __name__ == '__main__':
    main()