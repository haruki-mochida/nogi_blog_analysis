window.onload = function() {
    setInterval(function(){
        fetch('/progress')
        .then(response => response.text())
        .then(data => {
            document.getElementById('progress').innerText = 'Progress: ' + data + '%';
            if (parseInt(data) === 100) {
                window.location.href = '/analysis';
            }
        });
    }, 1000);  // 1000ミリ秒（1秒）ごとにリクエストを送る
};
