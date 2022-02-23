export const createSession = async (pool, id) => {
  await pool.query(`INSERT INTO session (id) VALUES ('${id}')`).catch((err) => {
    throw err;
  });
};

export const getSession = async (pool, id) => {
  const response = await pool.query(`SELECT * FROM session WHERE id = '${id}'`);
  return response.rows.length > 0 ? response.rows[0] : undefined;
};

export const updateTimer = (pool, sessionId) => {};

export const getTimer = (pool, sessionId) => {};
