function mostrar(tipo) {
    document.querySelector('.panel-imagenes').style.display = (tipo === 'imagenes') ? 'flex' : 'none';
    document.querySelector('.panel-detalle').style.display = 'flex';

    let items = document.querySelectorAll(`.item-imagen`);
    if (items.length > 0) seleccionarElemento(items[0], tipo);
}

function seleccionarElemento(elem, tipo) {
    let todos = document.querySelectorAll(`.item-imagen`);
    todos.forEach(item => item.classList.remove('selected'));

    elem.classList.add('selected');
    let src = elem.querySelector('img').getAttribute('src');
    let detalles = elem.querySelector('.info-imagen').getAttribute('data-details');

    document.getElementById('imagen-grande').style.display = 'block';
    document.getElementById('imagen-grande').src = src;
    document.getElementById('detalles-foto').innerHTML = detalles;
}

window.onload = function () {
    mostrar('imagenes');
}
