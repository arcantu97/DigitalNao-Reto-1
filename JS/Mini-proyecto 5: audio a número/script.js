
function playAudioByNumber(number){
    var colorsBg = ['blue', 'gray', 'green', 'red', 'orange'];
    var audio = document.getElementById('audio');
    audio.src = 'src/voice_' + number + '.mp3';
    audio.play();
    var numberText = document.getElementById('number-text');
    numberText.textContent = number;

    document.body.style.backgroundColor = colorsBg[number -  1];
}
