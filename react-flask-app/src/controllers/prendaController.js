const getPrendaByTipo = async function (tipo, setter, genero) {
  let requestOptions = {
    method: "GET",
    redirect: "follow",
  };

  let response =
    genero != null && tipo !== "Calzados"
      ? await fetch(
          `https://dressy-reporting-service.herokuapp.com/api/prendas/prendas/tipo/${tipo}/${genero}`,
          requestOptions
        )
      : await fetch(
          `https://dressy-reporting-service.herokuapp.com/api/prendas/prendas/tipo/${tipo}`,
          requestOptions
        );

  let data = await response.json();
  setter(data.listaPrendas);
  return data.listaPrendas;
};

const getPrendaByTipoAndGenero = async function (tipo, setter, genero) {
  let requestOptions = {
    method: "GET",
    redirect: "follow",
  };

  let response = await fetch(
    `https://dressy-reporting-service.herokuapp.com/api/prendas/prendas/tipo/${tipo}/${genero}`,
    requestOptions
  );

  let data = await response.json();
  setter(data.listaPrendas);
  return data.listaPrendas;
};

module.exports = {
  getPrendaByTipo,
  getPrendaByTipoAndGenero,
};
