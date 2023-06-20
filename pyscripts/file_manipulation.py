# -*- coding: utf-8 -*-
"""
File manipulation - misc tools for editing files
Author: steinhaug at gmail dot com
"""
import os
import sys
from collections.abc import Iterable, Sequence

KILL_CODE_FUNC = '''
import os; import signal;
def kill_process(msg):
    os.kill(os.getpid(), signal.SIGINT)
'''
KILL_CODE_BUTTON = '''    kill_name = gr.Textbox(label="Name",visible=False)
    kill_btn = gr.Button("Colab helper - Kill Running Process");
    kill_btn.click(fn=kill_process, inputs=kill_name, api_name="kill_process")
'''

# replacements = int, [int], or [(match_string, insert_string, ins_i)]
def insertInfrontWhenMatched(file_path, replacements):

    if not os.path.isfile( file_path ):
        print(f'Error opening file: {file_path}')
        sys.exit(1)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    if not isinstance(replacements, Sequence):
        replacements = [ replacements ]

    for my_object in replacements:
        if isinstance(my_object, Iterable):
            match_string, insert_string, ins_i = my_object
        else:
            if match_string == 1:
                match_string = 'with gr.Blocks(analytics_enabled=False) as demo:'
                insert_string = KILL_CODE_FUNC
                ins_i = 1
            elif match_string == 2:
                match_string = 'if shared.args.listen:'
                insert_string = KILL_CODE_BUTTON
                ins_i = 1

        for i, line in enumerate(lines):
            if match_string in line:
                lines.insert(i - ins_i, insert_string)
                break

    with open(file_path, 'w') as file:
        file.writelines(lines)


def commentOutLinesStartingWith(file_path, matches):

    if not os.path.isfile( file_path ):
        print(f'Error opening file: {file_path}')
        sys.exit(1)

    modified_lines = []

    with open(file_path, 'r') as file:
        #lines = file.readlines()
        # Read the file and modify the lines
        for line in file:
            line = line.strip()
            uncomment = False
            for match in matches:
                if line.startswith(match):
                    print(f'Match: {match}')
                    uncomment = True

            if uncomment:
                line = "# " + line

            modified_lines.append(line)

    # Save the modified lines back to the file
    with open(file_path, 'w') as file:
        file.write('\n'.join(modified_lines))


#if __name__ == '__main__':
#    main()

# commentOutLinesStartingWith('scripts/req.txt', ['soundfile'])
