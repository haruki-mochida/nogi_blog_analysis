// static/js/script.js
document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");

    // 解析待ちページであれば解析の進行状況を定期的に取得
    if (document.querySelector('#progress')) {
        setInterval(() => {
            fetch('/progress')
                .then(response => response.text())
                .then(progress => {
                    document.querySelector('#progress').textContent = progress;
                });
        }, 1000);  // 1秒ごとに取得
    }
});
