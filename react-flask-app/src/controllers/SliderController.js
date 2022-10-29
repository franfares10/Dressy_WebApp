//Generar el llamado que necesite

const postTermsAndGender = ()=>{
    let terminos = localStorage.getItem("terminos")
    let genero = localStorage.getItem("genero")
    var requestOptions = {
        method: 'POST',
        redirect: 'follow',
        mode:'no-cors'
      };
      
       fetch(`http://localhost:5000/termsAndConditions?terms=${terminos}&gender=${genero}`, requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
      
        console.log("Envio el genero y el estado legal")
}

export default postTermsAndGender;