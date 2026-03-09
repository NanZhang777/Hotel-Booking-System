export default function NumberField({ label, value, onChange, min=1, max=10 }){
  return (
    <div>
      <label className="small">{label}</label>
      <input
        className="input"
        type="number"
        value={value}
        min={min}
        max={max}
        onChange={e=> onChange(parseInt(e.target.value || '0', 10))}
      />
    </div>
  )
}