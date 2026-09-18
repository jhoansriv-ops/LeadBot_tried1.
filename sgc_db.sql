-- Ver total de registros
SELECT 'Clientes' AS tabla, COUNT(*) AS total FROM cliente
UNION ALL
SELECT 'Productos', COUNT(*) FROM producto
UNION ALL
SELECT 'Facturas', COUNT(*) FROM factura
UNION ALL
SELECT 'Detalles', COUNT(*) FROM factura_detalle;

-- Ver stock actualizado
SELECT codigo_sku, nombre, stock FROM producto ORDER BY id_producto;