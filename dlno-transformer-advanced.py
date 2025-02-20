import tkinter as tk
from tkinter import scrolledtext
import xml.etree.ElementTree as ET
import xml.dom.minidom
import pyperclip

def transform_word_xml(input_xml):
    try:
        root = ET.fromstring(input_xml.strip())
        if root.tag != "subst":
            raise ValueError("Root element must be <subst>")
        
        choice = ET.Element("choice", ana="author")
        
        choice1_seg = ET.Element("seg", type="choice1")
        choice2_seg = ET.Element("seg", type="choice2")
        
        for w in root.findall("w"):
            new_w = ET.Element("w", w.attrib)
            
            del_tag = w.find("del")
            add_tag = w.find("add")
            
            if del_tag is not None:
                # Preserve text content and subelements of <del>
                if del_tag.text:
                    new_w.text = del_tag.text  # Preserve text inside <del>
                for subelement in del_tag:
                    new_w.append(subelement)  # Move subelements to <w>
                choice1_seg.append(new_w)
            elif add_tag is not None:
                new_w.append(add_tag)  # Keep <add> as is
                choice2_seg.append(new_w)
        
        if len(choice1_seg):
            choice.append(choice1_seg)
        if len(choice2_seg):
            choice.append(choice2_seg)
        
        # Convert to string and pretty-print
        xml_string = ET.tostring(choice, encoding="unicode")
        parsed_xml = xml.dom.minidom.parseString(xml_string)
        pretty_xml = parsed_xml.toprettyxml(indent="    ")  # Adds line breaks & indentation
        
        # Remove the XML declaration (first line)
        pretty_xml = "\n".join(pretty_xml.split("\n")[1:])
        return pretty_xml.strip()
    
    except Exception as e:
        return f"Error: {e}"
    
def transform_inline_xml(input_xml):
    try:
        root = ET.fromstring(input_xml.strip())
        if root.tag != "subst":
            raise ValueError("Root element must be <subst>")
        
        choice = ET.Element("choice", ana="author")
        
        choice1_seg = ET.Element("seg", type="choice1")
        choice2_seg = ET.Element("seg", type="choice2")
        
        del_tag = root.find("del")
        add_tag = root.find("add")
        
        if del_tag is not None:
            if del_tag.text:
                choice1_seg.text = del_tag.text
            for subelement in del_tag:
                choice1_seg.append(subelement)
        
        if add_tag is not None:
            choice2_seg.append(add_tag)
        
        choice.append(choice1_seg)
        choice.append(choice2_seg)
        
        xml_string = ET.tostring(choice, encoding="unicode")
        parsed_xml = xml.dom.minidom.parseString(xml_string)
        pretty_xml = parsed_xml.toprettyxml(indent="    ")
        
        pretty_xml = "\n".join(pretty_xml.split("\n")[1:])
        return pretty_xml.strip()
    
    except Exception as e:
        return f"Error: {e}"

def convert():
    input_text = input_box.get("1.0", tk.END).strip()
    output_text = transform_inline_xml(input_text)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output_text)
    pyperclip.copy(output_box.get("1.0", tk.END).strip())

def clear_input_paste():
    input_box.delete("1.0", tk.END)

    # Get the clipboard contents
    clipboard_content = root.clipboard_get()
    
    # Insert clipboard content into the text box
    input_box.insert(tk.END, clipboard_content)

# GUI Setup
root = tk.Tk()
root.title("Thea's Excellent XML Converter")

# Input Text Box
tk.Label(root, text="Paste XML below:").pack()
input_box = scrolledtext.ScrolledText(root, height=10, width=80)
input_box.pack()

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack()

# Clear and Paste Button
tk.Button(button_frame, text="Clear and Paste", command=clear_input_paste, bg="#98D8EF").pack(side=tk.LEFT)

# Convert Button
tk.Button(button_frame, text="Convert and Copy", command=convert,bg="#CAE0BC").pack(side=tk.LEFT)

# Output Text Box
tk.Label(root, text="Converted XML:").pack()
output_box = scrolledtext.ScrolledText(root, height=10, width=80)
output_box.pack()


root.mainloop()
