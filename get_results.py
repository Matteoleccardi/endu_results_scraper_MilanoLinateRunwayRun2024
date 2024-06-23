import os, re, time


FILES_FOLDER = "C:\\Users\\lecca\\Downloads\\LinateRunwayRunWebpages\\"

if __name__ == "__main__":
    
    # I have a list of files it the folder FILES_FOLDER
    # of these files, i'm interested only in the ones that have the word "hours" in the content

    files = [
        f 
        for f in os.listdir(FILES_FOLDER)
        if f.endswith(".html") 
    ]

    # delete files that do not contain the word "hours" in it, since they do not contain the info we want

    for f in files:
        if not "hours" in open(FILES_FOLDER + f, encoding="utf8").read():
            os.remove(FILES_FOLDER + f)
            files.remove(f)

    files = [
        f
        for f in files
        if "hours" in open(FILES_FOLDER + f, encoding="utf8").read()
    ]

    # Now, for each file, I want to get the line number of the last occurrence of the word "hours"

    first_line = True
    for f in files:
        with open(FILES_FOLDER + f, encoding="utf8") as file:
            # get line number of last occurrence of "hours"
            for i, line in enumerate(file):
                if "hours" in line:
                    last_occurrence = i
            # now, get race times
            hours_line_delta = -9
            minutes_line_delta = -7
            seconds_line_delta = -5
            # now, hours, minutes and seconds are enclosed into, for example:
            # <td><span class="display displaygrey ng-binding">00</span></td>
            # i'm interested in the 00
            # I will use a regex to extract this information
            # hours
            hours_line = last_occurrence + hours_line_delta
            file.seek(0)
            for i, line in enumerate(file):
                if i == hours_line:
                    hours_line_content = line
            hours = re.search(r'>(\d+)<', hours_line_content).group(1)
            hours = int(hours)
            # minutes
            minutes_line = last_occurrence + minutes_line_delta
            file.seek(0)
            for i, line in enumerate(file):
                if i == minutes_line:
                    minutes_line_content = line
            minutes = re.search(r'>(\d+)<', minutes_line_content).group(1)
            minutes = int(minutes)
            # seconds
            seconds_line = last_occurrence + seconds_line_delta
            file.seek(0)
            for i, line in enumerate(file):
                if i == seconds_line:
                    seconds_line_content = line
            seconds = re.search(r'>(\d+)<', seconds_line_content).group(1)
            seconds = int(seconds)
            # total time in seconds
            total_time = hours * 3600 + minutes * 60 + seconds
            # ok now get the name of the person, which is enclosed in the <title> tag
            file.seek(0)
            for i, line in enumerate(file):
                if "<title>" in line:
                    title_line = line
            name = re.search(r'title>(.*) -', title_line).group(1).strip().replace("  ", " ").lower().title()
            # find sex
            file.seek(0)
            sex_line = None
            for i, line in enumerate(file):
                if "ng-src=\"/immagini/endu_athlete_" in line:
                    sex_line = line
            if sex_line is None:
                sex_char = "U"
                given_name_ = name.split(" ")[0].lower()
                if given_name_.endswith("o") or given_name_.endswith("e") or given_name_.endswith("i") or given_name_.endswith("drea"):
                    sex_char = "M"
                if given_name_.endswith("a"):
                    sex_char = "F"
            else:
                # ng-src="/immagini/endu_athlete_M.png"
                sex_char = re.search(r'ng-src="/immagini/endu_athlete_(.).png', sex_line)
                sex_char = sex_char.group(1).strip().upper()
            # find age
            # ng-class="{'M' : 'flaticon-mars', 'F' : 'flaticon-venus'}[performance.gender]" style="margin-right: 5px;"></span> <strong class="ng-binding">1980</strong></span>
            file.seek(0)
            age_line = None
            age_identifier_string = """ng-class="{'M' : 'flaticon-mars', 'F' : 'flaticon-venus'}[performance.gender]" style="margin-right: 5px;"></span> <strong class="ng-binding">"""
            for i, line in enumerate(file):
                if age_identifier_string in line:
                    age_line = line
            if age_line is not None:
                year_of_birth = re.search(
                    r'ng-class="{.*}.*strong class="ng-binding">(\d+)<',
                    age_line
                )
                year_of_birth = year_of_birth.group(1) if year_of_birth is not None else "0"
                year_of_birth = int(year_of_birth)
            else:
                year_of_birth = 0
            # save results
            file_id = f.replace(".html", "")
            str = f"{file_id}|{name}|{year_of_birth}|{sex_char}|{int(hours)}|{int(minutes)}|{int(seconds)}|{total_time}"
            if 0:
                print(str)
            else:
                file_results = "results.csv"
                if first_line:
                    with open(file_results, "w", encoding="utf8") as results:
                        results.write("file_id|name|year_of_birth|sex|hours|minutes|seconds|total_time\n")
                    first_line = False
                if not first_line:
                    with open(file_results, "a", encoding="utf8") as results:
                        results.write(str + "\n")
                    


            


