const start = document.querySelector('#start');
const pause = document.querySelector('#pause');
const stop = document.querySelector('#stop');
const recordingsList = document.querySelector('#recordings-list');
const submit = document.querySelector('#submit');
const base64_str = document.querySelector('#base_64_str');
const anchorTag = document.querySelector('#anchorTag');
const hiddenDiv = document.querySelector('#hiddenDiv');

var audStream;
var rec;
var input;

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext;

if(navigator.mediaDevices.getUserMedia){
    console.log('getUserMedia is not supported');

    let onSuccess = (stream) => {
        console.log('onSuccess(stream)');
        console.log(stream);
        audioContext = new AudioContext;
        audStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input, {numChannels:1});

        start.onclick = () => {
            console.log('recording started.');
            start.disabled=true;
            pause.disabled=false;
            stop.disabled=false;
            rec.record();
            Clock.start();
        }

        pause.onclick = () => {
            if(rec.recording){
                console.log('recording paused');
                rec.stop();
                Clock.pause();
                pause.textContent='Resume';
            }
            else{
                console.log('recording resumed');
                rec.record();
                Clock.resume();
                pause.textContent='Pause'
            }
        }

        stop.onclick = () => {
            console.log('stop.onclick()');
            pause.disabled=true;
            pause.textContent='Pause';
            stop.disabled=true;
            submit.disabled=false;
            rec.stop();
            Clock.stop();
            audStream.getAudioTracks()[0].stop();
            rec.exportWAV(createDownloadLink);//createDownloadLink is a function. We are sending this function to exportWav()
            rec.exportWAV(preSubmit);
        }
    }

    let onError = (error) => {
        console.log('Following Error occured');
        console.log(error);
    }

    constraintsObj = {
        audio: true,
        video: false,
    }
    navigator.mediaDevices.getUserMedia(constraintsObj).then(onSuccess).catch(onError)
}
else{
    console.log('getUserMedia is not supported');
}
