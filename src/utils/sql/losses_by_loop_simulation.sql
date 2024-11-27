SELECT losses.*
FROM losses
JOIN simulations ON losses.simulation_id = simulations.id
WHERE simulations.loop_simulation_id = 345
ORDER BY losses.simulation_id ASC;
