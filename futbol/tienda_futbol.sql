SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `usuarios` (
  `ID` int(200) NOT NULL,
  `contraseña` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `usuarios` (`ID`, `contraseña`, `email`) VALUES
(1, 'jon', 'jon@gmail.com'),
(2, 'juan', 'juan@ucompensar.com'),

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `usuarios`
  MODIFY `ID` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;
