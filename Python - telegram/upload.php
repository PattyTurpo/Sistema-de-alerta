<?php
$uploadDir = "uploads/";

// Asegurar que la carpeta de imágenes exista
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['fileToUpload'])) {
    $fileTmpPath = $_FILES['fileToUpload']['tmp_name'];
    $fileName = basename($_FILES['fileToUpload']['name']);
    $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

    // Validar solo imágenes
    if (in_array($fileExtension, ['jpg', 'jpeg', 'png'])) {
        $destination = $uploadDir . $fileName;
    } else {
        echo "❌ Solo se permiten archivos de imagen (jpg, jpeg, png).";
        exit;
    }

    // Mover archivo
    if (move_uploaded_file($fileTmpPath, $destination)) {
        echo "✅ Imagen subida correctamente.";
    } else {
        echo "❌ Error al guardar la imagen.";
    }
} else {
    echo "❌ No se recibió ningún archivo.";
}
?>
