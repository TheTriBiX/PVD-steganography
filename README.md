# PVD-steganography

Это PVD алгоритм для встраивания текста в изображения формата bmp
Реализован он так что берет в качестве пары подряд идущие байты цветов(то есть для первой пары это будут красный и зеленый цвет первого пикселя, для второй пары синий цвет первого пикселя и красный цвет второго пикселя) и увеличивает или не изменят разницу между ними(в зависимости от бита который мы встриваем)

Количество информации которую мы можем зашифровать равна (3 * n / 2) бит, где n - это количество пикселей в изображении
