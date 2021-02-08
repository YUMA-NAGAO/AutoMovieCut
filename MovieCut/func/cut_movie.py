import time
import os
import subprocess



def get_movie(wk_dir):
    files = os.listdir(wk_dir)
    files = natsort.natsorted([x for x in files if x[-4:] == ".MOV" or x[-4:] == ".mp4" or x[-4:] == ".mov"])
    return files


def output_silent(movie1, dB1):
    os.chdir("../input")
    output = subprocess.run(
        ["ffmpeg", "-i", movie1, "-af", "silencedetect=noise={}dB:d=0.3".format(dB1), "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ss = str(output)
    lines = ss.replace("\\r", "")
    lines = lines.split('\\n')
    time_list = []
    for line1 in lines:
        if "silencedetect" in line1:
            words1 = line1.split(" ")
            for i in range(len(words1)):
                if "silence_start" in words1[i]:
                    time_list.append(float(words1[i + 1]))
                if "silence_end" in words1[i]:
                    time_list.append(float(words1[i + 1]))
    silence_section_list = list(zip(*[iter(time_list)] * 2))
    movie_name = movie1.split(".")
    """if str(silence_section_list[0][0]) != "0.0":
        split_file1 = "../output/" + movie_name[0] + "_0" + ".mp4"
        subprocess.run(["ffmpeg", "-ss", str(0), "-i", movie1, "-t", str(silence_section_list[1][0]), split_file1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)"""

    for i in range(len(silence_section_list) - 1):
        split_file = "../output/" + movie_name[0] + "_" + str(i + 1) + ".mp4"
        subprocess.run(["ffmpeg", "-ss", str(silence_section_list[i][1]), "-i", movie1, "-t", str(silence_section_list[i + 1][0] - silence_section_list[i][1]), split_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(movie_name[0] + "_" + str(i + 1) + ".mp4")



if __name__ == "__main__":
    subprocess.run(["mkdir","../output"])

    movie_list = get_movie("../input")
    start =time.time()
    for movie in movie_list:
        print("処理する動画")
        print(movie)
        dB = input("カットする音量の閾値を入力(dB)、デフォルトの場合はそのままエンター ※デフォルト-33dB>", )
        if dB == "":
            dB = "-33"
        output_silent(movie, dB)

    movie_list = get_movie("../output")
    for movie in movie_list:
        output_file = subprocess.run(["ffmpeg", "-i", movie, "-f", "h264_videotoolbox", "-"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        s = str(output_file)
        lines1 = s.replace("\\r", "")
        lines1 = lines1.split('\\n')
        os.chdir("../output")
        for line in lines1:
            if "Duration" in line:
                words = line.split(" ")
                word = words[3].split(":")[2]
                word = word.replace(",", "")
                if float(word) < 0.5:
                    os.remove(movie)

    ProcessTime=time.time()-start

    print(ProcessTime)

