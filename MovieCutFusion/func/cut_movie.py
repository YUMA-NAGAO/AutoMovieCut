import time
import os
import subprocess
import natsort


def get_movie(wk_dir):
    files = os.listdir(wk_dir)
    files = natsort.natsorted([x for x in files if x[-4:] == ".MOV" or x[-4:] == ".mp4" or x[-4:] == ".mov"])
    return files


def cut_silent(movie1, dB1):
    os.chdir("../input")
    cut = subprocess.run(
        ["ffmpeg", "-i", movie1, "-af", "silencedetect=noise={}dB:d=0.3".format(dB1), "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ss = str(cut)
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

    for i in range(len(silence_section_list) - 1):
        split_file = "../cut/" + movie_name[0] + "_" + str(i + 1) + ".mp4"
        subprocess.run(["ffmpeg", "-ss", str(silence_section_list[i][1]), "-i", movie1, "-t", str(silence_section_list[i + 1][0] - silence_section_list[i][1]), split_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(movie_name[0] + "_" + str(i + 1) + ".mp4")


def merge_movie(movie_list1):
    os.chdir("../cut")
    FileName="out.mp4"
    movie_list1 = [ m for m in movie_list1]
    with open("tmp.txt", "w") as fp:
        lines = [f"file '{line1}'" for line1 in movie_list1]
        fp.write("\n".join(lines))
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "tmp.txt", "-c", "copy",FileName ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["mkdir","../merged"])
    subprocess.run(["mv","out.mp4","../merged"])


if __name__ == "__main__":
    start =time.time()
    subprocess.run(["mkdir","../cut"])
    input_movie = get_movie("../input")

    for movie in input_movie:
        print("処理する動画")
        print(movie)
        dB = input("カットする音量の閾値を入力(dB)、デフォルトの場合はそのままエンター ※デフォルト-33dB>", )
        if dB == "":
            dB = "-33"
        cut_silent(movie, dB)

    movie_list = get_movie("../cut")
    for movie in movie_list:
        cut_file = subprocess.run(["ffmpeg", "-i", movie, "-f", "h264_videotoolbox", "-"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        s = str(cut_file)
        lines1 = s.replace("\\r", "")
        lines1 = lines1.split('\\n')
        os.chdir("../cut")
        for line in lines1:
            if "Duration" in line:
                words = line.split(" ")
                word = words[3].split(":")[2]
                word = word.replace(",", "")
                if float(word) < 0.5:
                    os.remove(movie)


    merge_movie(movie_list)

    ProcessTime=time.time()-start
    minutes=str(ProcessTime//60)
    second=str((ProcessTime%60)//1)

    print(minutes+"分"+second+"秒")
