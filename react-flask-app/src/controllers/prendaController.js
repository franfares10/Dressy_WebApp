import React from "react";

const getPrendaByTipo = async function (tipo,setter){
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };
      
     let response = await fetch(`https://dressy-reporting-service.herokuapp.com/api/prendas/prendas/tipo/${tipo}`, requestOptions)

    
    let data = await response.json();
    setter(data.listaPrendas)
    return data.listaPrendas;
}

export default getPrendaByTipo;