from pathlib import Path
import numpy as np
import librosa
import concurrent
import soundfile as sf
import xml.etree.ElementTree as ET




def breakfile(file, tree):
    
    
    file = Path(file)
    aud, sr = librosa.load(file, sr = None)
    aud = librosa.resample(aud, sr, 32000)
    sr = 32000
    outpath = path
    
    
    
    doc = open('reference.txt', 'a')
    i = 0
    e_ = 0
    
    for x in tree.findall('./events/item'):
        for child in x:

            if child.tag == "PATHNAME":
                path_ = child.text
                
            elif child.tag == "CLASS_ID":
                class_ = int(child.text)

            elif child.tag == "CLASS_NAME":
                tag_ = child.text
                tag_ = tag_.split('/')[0]
                
            elif child.tag == "STARTSECOND":
                s_ = float(child.text)
                if(s_-e_>0):
                    if( (s_-e_)<10):
                        outfile = 'tr_'+file.stem+"_bck_{}.wav".format(i)
                        x = outpath/Path('background')
                        x.mkdir(exist_ok = True)
                        sf.write(x/outfile, aud[int(e_*sr): int(s_*sr)], sr)
    #                     doc.write( "{}\t{}\n".format(outfile, '1') )
                        i+=1
                    else:
                        outfile = 'tr_'+file.stem+"_bck_{}.wav".format(i)
                        x = outpath/Path('background')
                        x.mkdir(exist_ok = True)
                        sf.write(x/outfile, aud[int(e_*sr): int((e_+9)*sr)], sr)
    #                     doc.write( "{}\t{}\n".format(outfile, '1') )
                         
            elif child.tag == "ENDSECOND":
                e_ = float(child.text)
                
                outfile = 'tr_'+file.stem + "_" + str(path_ )

                x = outpath/Path('car_crash' if class_ == 3 else 'car_skid' )
                x.mkdir( exist_ok = True )
                s = int(np.floor(s_))
                e = int(np.ceil(e_))
#                 print(s)
                sf.write(x/outfile,   aud[ s*sr:e*sr], sr)
                
            
#                 doc.write( "{}\t{}\n".format(outfile, int(class_)+3) )
                
with concurrent.futures.ThreadPoolExecutor() as TPE:
 
    path = "/path/to/MIVIA_ROAD_DB1/"
    path = Path(path)
    files = glob( os.path.join(path,'*.xml'))
    for file in files:
        file = Path(file)
        filename = file.stem
        tree = ET.parse(file)
        
        audios = glob(os.path.join('./',file.parent,"sounds",filename+'*'))
        for audio in audios:
            TPE.submit(breakfile(audio,tree))
       
        

            
            
