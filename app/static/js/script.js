window.onload = function() {
    // intervalIDを変数で保持する
    const intervalID = setInterval(function(){
        fetch('/progress')
        .then(response => response.text())
        .then(data => {
            document.getElementById('progress').innerText = 'Progress: ' + data + '%';
            if (parseInt(data) === 100) {
                // 進捗が100%に達した場合、ポーリングを停止する
                clearInterval(intervalID);
                window.location.href = '/analysis';
            }
        })
        .catch(error => {
            console.error('Error fetching progress:', error);
        });
    }, 1000);
};
