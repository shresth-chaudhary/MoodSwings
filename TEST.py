{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING:root:frame length (960) is greater than FFT size (512), frame will be truncated. Increase NFFT to avoid.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "hip hop\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "'C:/Users/Shresth/Music/hip hop\\\\abc.wav'"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from python_speech_features import mfcc\n",
    "import scipy.io.wavfile as wav\n",
    "import numpy as np\n",
    "from tempfile import TemporaryFile\n",
    "import os\n",
    "import pickle\n",
    "import random \n",
    "import operator\n",
    "import math\n",
    "import numpy as np\n",
    "from collections import defaultdict\n",
    "dataset = []\n",
    "\n",
    "def loadDataset(filename):\n",
    "    with open(\"my.dat\" , 'rb') as f:\n",
    "        while True:\n",
    "            try:\n",
    "                dataset.append(pickle.load(f))\n",
    "            except EOFError:\n",
    "                f.close()\n",
    "                break\n",
    "loadDataset(\"my.dat\")\n",
    "\n",
    "def distance(instance1 , instance2 , k ):\n",
    "    distance =0 \n",
    "    mm1 = instance1[0] \n",
    "    cm1 = instance1[1]\n",
    "    mm2 = instance2[0]\n",
    "    cm2 = instance2[1]\n",
    "    distance = np.trace(np.dot(np.linalg.inv(cm2), cm1)) \n",
    "    distance+=(np.dot(np.dot((mm2-mm1).transpose() , np.linalg.inv(cm2)) , mm2-mm1 )) \n",
    "    distance+= np.log(np.linalg.det(cm2)) - np.log(np.linalg.det(cm1))\n",
    "    distance-= k\n",
    "    return distance\n",
    "\n",
    "def getNeighbors(trainingSet , instance , k):\n",
    "    distances =[]\n",
    "    for x in range (len(trainingSet)):\n",
    "        dist = distance(trainingSet[x], instance, k )+ distance(instance, trainingSet[x], k)\n",
    "        distances.append((trainingSet[x][2], dist))\n",
    "    distances.sort(key=operator.itemgetter(1))\n",
    "    neighbors = []\n",
    "    for x in range(k):\n",
    "        neighbors.append(distances[x][0])\n",
    "    return neighbors  \n",
    "\n",
    "def nearestClass(neighbors):\n",
    "    classVote ={}\n",
    "    for x in range(len(neighbors)):\n",
    "        response = neighbors[x]\n",
    "        if response in classVote:\n",
    "            classVote[response]+=1 \n",
    "        else:\n",
    "            classVote[response]=1 \n",
    "    sorter = sorted(classVote.items(), key = operator.itemgetter(1), reverse=True)\n",
    "    return sorter[0][0]\n",
    "\n",
    "results = {1:'disco', 2:'rock', 3:'blues', 4: 'metal', 5:'hip hop', 6:'classical', 7: 'reggae', 8: 'jazz', 9:'country', 10:'pop'}\n",
    "\n",
    "file=wav.read(\"C:/Users/Shresth/Music/test audio/abc.wav\")\n",
    "    \n",
    "(rate,sig)=file\n",
    "mfcc_feat=mfcc(sig,rate,winlen=0.020,appendEnergy=False)\n",
    "covariance = np.cov(np.matrix.transpose(mfcc_feat))\n",
    "mean_matrix = mfcc_feat.mean(0)\n",
    "feature=(mean_matrix,covariance,0)\n",
    "\n",
    "pred=nearestClass(getNeighbors(dataset ,feature , 5))\n",
    "\n",
    "print(results[pred])\n",
    "import shutil, os\n",
    "xh = str(results[pred])\n",
    "shutil.move(\"C:/Users/Shresth/Music/test audio/abc.wav\",'C:/Users/Shresth/Music/' + xh)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
