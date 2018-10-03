# audio_coder 

This is a repository containing a solution to the following task that was given in a universiy-course.

## Task
The goal of the lab is to construct a lossy coder and decoder for music data. The coder should meet given demands on distortion and rate when coding the test music.

## Demands
* At a rate of at most 192 kbit/s the signal-to-noise ratio (measured over the whole song) when coding the two test song should be at least 30 dB. The cost of all side information (quantization parameters, code trees, et c.) must be included in the rate. 
* The coder should be general, ie it should be able to code any music and not just the two test songs, giving roughly the same results. 
* The coding must be done in such a way that when decoding you can jump to any position in the song without having to decode all the data up to this position. In order to do this, the data should be coded in blocks of at most 4096 stereo samples (4096 samples from the left and the right channel). This will limit the size of any transforms used and also means that any adaptive coding can only depend on the data inside the block. It is allowed to let any variable length codes and quantization parameters depend on all of the file. These parameters can be seen as header information that is sent once at the beginning of the file. 

## Test data
The music files to be coded can be found on [http://www.icg.isy.liu.se/courses/tsbk02/music/].
The music is in stereo, 16 bits per sample, sampling frequency 44.1 kHz. The raw data rate is thus 1411.2 kbit/s.
The files are available as complete WAV files and also split into smaller parts. 
