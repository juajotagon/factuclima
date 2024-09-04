$(document).ready(function(){
    $("#send-invoice-form").on("submit", function(event){
        event.preventDefault();  // Previene el envío tradicional
        console.log("Formulario interceptado");  // Verificación de intercepción

        $.ajax({
            url: $(this).attr("action"),
            type: "POST",
            data: $(this).serialize(),  // Serializa los datos del formulario
            success: function(response) {
                if (response.status === 'success') {
                    $("#email-status").html('<div class="alert alert-success">Correo enviado el: ' + response.fecha_envio + '</div>');
                } else {
                    $("#email-status").html('<div class="alert alert-danger">Error al enviar el correo: ' + response.message + '</div>');
                }
            },
            error: function() {
                $("#email-status").html('<div class="alert alert-danger">Error al enviar el correo.</div>');
            }
        });
    });
});

function agregarProducto() {
    const productosDiv = document.getElementById('productos');
    const nuevoProducto = document.createElement('div');
    nuevoProducto.classList.add('producto', 'form-row');

    nuevoProducto.innerHTML = `
        <div class="form-group col-md-6">
            <label for="nombre_producto">Nombre del Producto:</label>
            <input type="text" name="nombre_producto[]" class="form-control" required>
        </div>
        <div class="form-group col-md-6">
            <label for="precio_producto">Precio del Producto:</label>
            <input type="number" name="precio_producto[]" class="form-control" min="0.01" step="0.01" required>
        </div>
    `;

    productosDiv.appendChild(nuevoProducto);
}
