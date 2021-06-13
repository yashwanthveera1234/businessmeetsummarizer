var createDownloadLink = (blob) => {
    var audioUrl = URL.createObjectURL(blob);
    var audioTag = document.createElement('audio');

    var filename = new Date().toISOString();

    audioTag.controls = true;
    audioTag.src = audioUrl;

    anchorTag.href = audioUrl;
    anchorTag.download = filename+'.wav';

    recordingsList.appendChild(audioTag);
    hiddenDiv.hidden = false;
}
