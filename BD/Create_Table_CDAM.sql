-- creacion de tablas
--Dari

--Usuario
create type nom_completo as (
	nombre varchar(50),
	ap_paterno varchar (50),
	ap_materno varchar(50)
);

create type rango as enum (
	'Novato', 'Junior', 'Intermedio', 'Semi Senior', 'Experto', 'Senior'
);

create table Usuarios (
	id_user serial primary key,
	nombre nom_completo,
	username varchar(50) unique, --el que elija el usuario
	contraseña varchar(100), -- se ocultara desde el codigo
	correo varchar (100) unique, --seleccionado por el usuario
	nivel_usuario  rango default 'Novato',
	imagen varchar (100),
	fecha_registro date default current_date
);

-- capitulo
create table Capitulos (
	id_cap serial primary key,
	nombre varchar (100),
	descripcion text,
	icono varchar (100),
	orden int unique not null --secuencia
);

--nivel
create type tipos as enum (
	'Teoria', 'Ejercicio', 'Desafio'
);

create table Niveles (
	id_nivel serial primary key,
	id_cap int references Capitulos(id_cap),
	tipo tipos,
	titulo varchar (100),
	puntos_recompensa int,
	orden int not null
);

create table Niveles_Teoria(
	id_lvT int primary key references Niveles(id_nivel),
	contenido text not null
);

create table Niveles_Ejercicios (
	id_lvE int primary key references Niveles(id_nivel),
	enunciado text not null,
	solucion text not null
);

create table Casos_Prueba ( -- verificar ejecutando codigo de usuario y si la salida es igual es correcto
	id_test serial primary key,
	id_lvl int references Niveles_Ejercicios(id_lvE),
	input text,
	output text
);

--Personajes
create table Personajes (
	id_npc serial primary key,
	nombre varchar(100),
	descripcion text,
	imagen varchar (100),
	id_lvT_unlock int references Niveles_Teoria(id_lvT)
);

-- Items
create table Items (
	id_item serial primary key,
	nombre varchar(50),
	descripcion text,
	imagen varchar (100),
	max_usos int, --se puede usar unas cauntas veces dentro del cap, un nuevo cap se regenera
	id_personaje int references Personajes(id_npc)
);

create table Uso_item (
	id_uso serial primary key,
	id_usuario int references Usuarios (id_user),
	id_items int references Items(id_item),
	id_capi int references Capitulos(id_cap),
	id_lvl int references Niveles(id_nivel)
);

--mochila estos se agregan dentro del codigo 
create table Mochila_per (
	id_MP serial primary key,
	id_usuario int references Usuarios(id_user),
	id_personaje int references Personajes(id_npc),
	fecha date
);

create table Mochila_It (
	id_MI serial primary key,
	id_usuario int references Usuarios (id_user),
	id_item int references Items(id_item),
	fecha date
);

--progreso 
create table Progreso (
	id_progreso serial primary key,
	id_usuario int references Usuarios (id_user),
	cap_act int references Capitulos(id_cap),
	lvl_act int references Niveles(id_nivel),
	exp_total int default 0
);

CREATE TABLE Niveles_Completados (
    id_completado SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES Usuarios(id_user),
    id_nivel INT NOT NULL REFERENCES Niveles(id_nivel),
    completado BOOLEAN NOT NULL DEFAULT TRUE,
    puntos_obtenidos INT NOT NULL,
    intentos INT DEFAULT 1,
    fecha_completado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	 UNIQUE(id_usuario, id_nivel) 
);

