CREATE TABLE Editorial(
    editorial_id SERIAL,
    nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (editorial_id)
);


CREATE TABLE Libro (
    libro_id SERIAL,
    titulo VARCHAR(50) NOT NULL,
    autor VARCHAR(50)  NOT NULL,
    esta_disponible BOOLEAN NOT NULL,
    editorial_id INTEGER NOT NULL,
    PRIMARY KEY (libro_id),
    FOREIGN KEY (editorial_id) REFERENCES Editorial (editorial_id)
);


CREATE TABLE Lector (
    lector_id SERIAL,
    nombre VARCHAR(50) NOT NULL,
    dni CHAR(8) NOT NULL,
    PRIMARY KEY (lector_id)
);


CREATE TABLE Prestamo (
    prestamo_id SERIAL,
    fecha_prestamo DATE,
    fecha_devolucion DATE,
    lector_id INTEGER NOT NULL,
    libro_id INTEGER NOT NULL,
    PRIMARY KEY (prestamo_id),
    FOREIGN KEY (libro_id) REFERENCES Libro (libro_id),
    FOREIGN KEY (lector_id) REFERENCES Lector (lector_id)
);

