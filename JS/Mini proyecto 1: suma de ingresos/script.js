var compras = [];

// document.getElementById('agregarCompra').addEventListener('click', agregarCompra);

function agregarCompra() {
  var detalle = document.getElementById('detalleInput').value;
  var monto = document.getElementById('montoInput').value;
  if (detalle.trim() !== '' && monto.trim() !== '') {
    compras.push({ detalle: detalle, monto: parseFloat(monto).toFixed(2) }); 

    var tabla = document.getElementById('tablaCompras');

    var fila = tabla.insertRow();
    var celdaNombre = fila.insertCell();
    var celdaMonto = fila.insertCell();

    celdaNombre.innerHTML = detalle;
    celdaMonto.innerHTML = monto;
    

    var totalCell = document.getElementById('total');
    totalCell.style.backgroundColor = "yellow";
    totalCell.innerHTML = calcularTotal();

    document.getElementById('detalleInput').value = '';
    document.getElementById('montoInput').value = '';
  } else {
    window.alert(detalle.trim() === '' ? 
    "El campo 'descripción del ingreso' no puede estar vacío!" : 
    "El campo 'monto del ingreso' no puede estar vacío!");
  }
}

function calcularTotal(){
  // El operador "+" antes de la propiedad castea como Number en la operación.
  return compras.reduce((total, compra) =>  +total + +compra.monto, 0.0);
}
