--triggers

--inizializamos el progresp
CREATE OR REPLACE FUNCTION inicializar_progreso_usuario()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Progreso (id_usuario, cap_act, lvl_act)
    VALUES (
        NEW.id_user, 
        (SELECT id_cap FROM Capitulos ORDER BY orden ASC LIMIT 1),
        (SELECT id_nivel FROM Niveles ORDER BY orden ASC LIMIT 1)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--actualizar cap y lvl
CREATE OR REPLACE FUNCTION actualizar_progreso()
RETURNS TRIGGER AS $$
DECLARE
    siguiente_nivel INT;
    siguiente_capitulo INT;
    cap_actual INT;
    nivel_actual INT;
BEGIN
    -- Obtener el progreso actual del usuario
    SELECT cap_act, lvl_act INTO cap_actual, nivel_actual
    FROM Progreso WHERE id_usuario = NEW.id_usuario;
    
    IF NEW.completado = TRUE THEN
        -- Buscar siguiente nivel en el mismo capítulo
        SELECT id_nivel INTO siguiente_nivel
        FROM Niveles
        WHERE id_cap = cap_actual AND orden > (
            SELECT orden FROM Niveles WHERE id_nivel = nivel_actual
        )
        ORDER BY orden ASC LIMIT 1;
        
        IF siguiente_nivel IS NOT NULL THEN
            UPDATE Progreso
            SET lvl_act = siguiente_nivel  -- Eliminado ultimo_acceso
            WHERE id_usuario = NEW.id_usuario;
        ELSE
            -- Buscar siguiente capítulo
            SELECT id_cap INTO siguiente_capitulo
            FROM Capitulos
            WHERE orden > (SELECT orden FROM Capitulos WHERE id_cap = cap_actual)
            ORDER BY orden ASC LIMIT 1;
            
            IF siguiente_capitulo IS NOT NULL THEN
                SELECT id_nivel INTO siguiente_nivel
                FROM Niveles
                WHERE id_cap = siguiente_capitulo
                ORDER BY orden ASC LIMIT 1;
                
                UPDATE Progreso
                SET cap_act = siguiente_capitulo,
                    lvl_act = siguiente_nivel  -- Eliminado ultimo_acceso
                WHERE id_usuario = NEW.id_usuario;
            END IF;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--sumar experiencia
CREATE OR REPLACE FUNCTION sumar_experiencia_nivel()
RETURNS TRIGGER AS $$
BEGIN
    -- Suma los puntos del nivel completado
    UPDATE Progreso
    SET exp_total = exp_total + NEW.puntos_obtenidos
    WHERE id_usuario = NEW.id_usuario;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--actualizar rango
CREATE OR REPLACE FUNCTION actualizar_rango_usuario()
RETURNS TRIGGER AS $$
DECLARE
    nuevo_rango rango;
BEGIN
    IF NEW.exp_total >= 500 THEN
        nuevo_rango := 'Senior';
    ELSIF NEW.exp_total >= 300 THEN
        nuevo_rango := 'Experto';
    ELSIF NEW.exp_total >= 200 THEN
        nuevo_rango := 'Semi Senior';
    ELSIF NEW.exp_total >= 100 THEN
        nuevo_rango := 'Intermedio';
    ELSIF NEW.exp_total >= 50 THEN
        nuevo_rango := 'Junior';
    ELSE
        nuevo_rango := 'Novato';
    END IF;
    
    UPDATE Usuarios
    SET nivel_usuario = nuevo_rango
    WHERE id_user = NEW.id_usuario AND nivel_usuario != nuevo_rango;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_inicializar_progreso
AFTER INSERT ON Usuarios
FOR EACH ROW EXECUTE FUNCTION inicializar_progreso_usuario();

CREATE TRIGGER tr_actualizar_progreso
AFTER INSERT ON Niveles_Completados
FOR EACH ROW EXECUTE FUNCTION actualizar_progreso();

CREATE TRIGGER tr_sumar_experiencia
AFTER INSERT ON Niveles_Completados
FOR EACH ROW EXECUTE FUNCTION sumar_experiencia_nivel();

CREATE TRIGGER tr_actualizar_rango
AFTER UPDATE OF exp_total ON Progreso
FOR EACH ROW EXECUTE FUNCTION actualizar_rango_usuario();

ALTER TABLE Progreso
ALTER COLUMN cap_act SET NOT NULL,
ALTER COLUMN lvl_act SET NOT NULL;

CREATE OR REPLACE FUNCTION inicializar_progreso_usuario()
RETURNS TRIGGER AS $$
DECLARE
    primer_capitulo INT;
    primer_nivel INT;
BEGIN
    SELECT id_cap INTO primer_capitulo FROM Capitulos ORDER BY orden ASC LIMIT 1;
    SELECT id_nivel INTO primer_nivel FROM Niveles ORDER BY orden ASC LIMIT 1;

    IF primer_capitulo IS NOT NULL AND primer_nivel IS NOT NULL THEN
        INSERT INTO Progreso (id_usuario, cap_act, lvl_act)
        VALUES (NEW.id_user, primer_capitulo, primer_nivel);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

