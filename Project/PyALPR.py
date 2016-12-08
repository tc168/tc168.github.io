import json, shlex, subprocess

class PlateReader:


    def __init__(self):
        #webcam subprocess args
        webcam_command = "sudo dd if=/dev/video0 of=alpr.jpeg bs=11M count=1"
        self.webcam_command_args = shlex.split(webcam_command)

        #alpr subprocess args
        alpr_command = "sudo alpr -c us  -n 2 -j alpr.jpeg"
        self.alpr_command_args = shlex.split(alpr_command)


    def webcam_subprocess(self):
        return subprocess.Popen(self.webcam_command_args, stdout=subprocess.PIPE,shell=False)


    def alpr_subprocess(self):
        return subprocess.Popen(self.alpr_command_args, stdout=subprocess.PIPE,shell=False)


    def alpr_json_results(self):
        self.webcam_subprocess().communicate()
        alpr_out, alpr_error = self.alpr_subprocess().communicate()

        if "No license plates found." in alpr_out:
            return None, None

        try:
            return json.loads(alpr_out), None
        except ValueError, e:
            return None, e


    def read_plate(self):
        alpr_json, alpr_error = self.alpr_json_results()

        if not alpr_error is None:
            print alpr_error
            return
        

        if alpr_json is None:
            print "No results!"
            return

        results = alpr_json["results"]

        ordinal = 0
        for result in results:
            candidates = result["candidates"]

            for candidate in candidates:
                if candidate["matches_template"] == 1:
                    ordinal += 1
                    print "Guess {0:d}: {1:s} {2:.2f}%".format(ordinal, candidate["plate"], candidate["confidence"])


if __name__=="__main__":
    plate_reader = PlateReader()
    plate_reader.read_plate()
