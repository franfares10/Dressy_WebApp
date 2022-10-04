const stopThreads =  (prenda,estado) =>{
    var requestOptions = {
        method: 'POST',
        redirect: 'follow',
        mode:'no-cors'
      };
      
       fetch(`http://localhost:5000/stop_video`, requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
      
        console.log("MANDE ESTADO 0")
}

export default stopThreads;