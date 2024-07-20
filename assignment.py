import os

def read_ass_file(file_path): # read_ass_file -> Opens a file, reads all lines into a list, and returns this list.
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def write_ass_file(file_path, content): # write_ass_file -> Opens a file, writes the given list of lines to the file, and ensures the file is properly closed.
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

def transform_subtitles(lines):
    # Find the start of the Events section - 
    events_start_index = lines.index("[Events]\n")
    events_format = lines[events_start_index + 1]
    events = lines[events_start_index + 2:]
    
    transformed_events = []

    for i, event in enumerate(events):
        #If the current event is the first one (i == 0), it adds a placeholder line for the previous line.
        if i == 0:
            transformed_events.append('Dialogue: 0,0:00:00.00,0:00:00.00,P,,0,0,0,,...\n')
            #Otherwise, it adds the actual previous event, replacing Default with P to indicate it's the previous line.
        else:
            prev_event = events[i - 1]
            transformed_events.append(prev_event.replace('Default', 'P'))
        
        # Add current event
        transformed_events.append(event)
        
        # If the current event is the last one (i == len(events) - 1), it adds a placeholder line for the next line.

        if i == len(events) - 1:
            transformed_events.append('Dialogue: 0,0:00:00.00,0:00:00.00,F,,0,0,0,,...\n')
            # Else, it adds the actual next event, replacing Default with F to indicate it's the next line.
        else:
            next_event = events[i + 1]
            transformed_events.append(next_event.replace('Default', 'F'))
        
        transformed_events.append('\n')

    return lines[:events_start_index + 2] + transformed_events

def main():
    # Construct paths using os.path
    base_dir = r"F:\Desktop files\Playstudio assign"  # Defines the base directory for the subtitle files.
    input_file = os.path.join(base_dir, "input_subtitles.ass")  # Constructs the full paths for the input and output subtitle files.
    output_file = os.path.join(base_dir, "output_subtitles_.ass")
    input_lines = read_ass_file(input_file) #Reads the lines from the input subtitle file.
    output_lines = transform_subtitles(input_lines) #Transforms these lines to include previous and next events for each event.
    write_ass_file(output_file, output_lines) #Writes the transformed lines to the output subtitle file.

if __name__ == "__main__":
    main()
