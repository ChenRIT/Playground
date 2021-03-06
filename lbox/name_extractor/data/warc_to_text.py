# Convert a ClueWeb warc file into a text file

import warc

if __name__ == "__main__":
    input_file = "./00.warc.gz"
    output_fname = "./web_contents.txt"
    with open(output_fname, "w+") as ofile:
        fwarc = warc.open(input_file, "rb")
        for record in fwarc:
            if record['Warc-type'] == 'warcinfo':
                pass
            else:
                ofile.write(record.payload.encode('utf-8') + "\n")
            
