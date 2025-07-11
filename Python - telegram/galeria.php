<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <title>Galería de Imágenes - Proyecto Redes</title>
    <link rel="stylesheet" href="estilos.css">
</head>

<body>
    <div class="barra-lateral">
        <h2>📁 Menú</h2>
        <button onclick="mostrar('imagenes')">Ver Imágenes</button>
    </div>

    <div class="contenido-principal">
        <div class="panel-imagenes">
            <?php
            function nombreMes($n) {
                $meses = [1=>"Enero",2=>"Febrero",3=>"Marzo",4=>"Abril",5=>"Mayo",6=>"Junio",7=>"Julio",8=>"Agosto",9=>"Septiembre",10=>"Octubre",11=>"Noviembre",12=>"Diciembre"];
                return $meses[$n] ?? "Desconocido";
            }

            $imagenes = glob("uploads/*.{jpg,jpeg,png}", GLOB_BRACE);
            usort($imagenes, fn($a,$b) => filemtime($b) - filemtime($a));

            $mes_anterior = "";
            foreach ($imagenes as $img) {
                $fecha = filemtime($img);
                $mes = date("m", $fecha);
                $anio = date("Y", $fecha);
                $mes_actual = "$mes-$anio";
                if ($mes_actual !== $mes_anterior) {
                    echo "<div class='titulo-mes'>".nombreMes(intval($mes))." $anio</div>";
                    $mes_anterior = $mes_actual;
                }
                $fecha_fmt = date("d/m/Y H:i:s", $fecha);
                $detalles = "<strong>Fecha:</strong> ".nombreMes(intval($mes))." ".date("d", $fecha).", $anio<br><strong>Hora:</strong> ".date("H:i:s", $fecha);
                echo "<div class='item-imagen' onclick=\"seleccionarElemento(this, 'imagenes')\">";
                echo "<img src='$img' />";
                echo "<div class='info-imagen' data-details=\"$detalles\">$fecha_fmt</div>";
                echo "</div>";
            }
            ?>
        </div>

        <div class="panel-detalle">
            <img id="imagen-grande" style="display:none;" />
            <div class="detalles-foto" id="detalles-foto">Aquí aparecerán los detalles</div>
        </div>
    </div>
        <script src="funciones.js" defer></script>

</body>
</html>
