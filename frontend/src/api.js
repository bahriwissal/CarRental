async function request(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    const detail = Array.isArray(body.detail) ? body.detail.map((d) => d.msg).join(', ') : body.detail
    throw new Error(detail || `Request failed (${res.status})`)
  }
  return res.status === 204 ? null : res.json()
}

export const api = {
  listCars: () => request('/cars'),
  getCar: (id) => request(`/cars/${id}`),
  listBookings: () => request('/bookings'),
  createBooking: (data) => request('/bookings', { method: 'POST', body: JSON.stringify(data) }),
  cancelBooking: (id) => request(`/bookings/${id}`, { method: 'DELETE' }),
}
