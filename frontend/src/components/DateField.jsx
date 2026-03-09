export default function DateField({ label, value, onChange, min }){
  return (
    <div>
      <label className="small">{label}</label>
      <input
        className="input"
        type="date"
        value={value}
        min={min}
        onChange={e => onChange(e.target.value)}
      />
    </div>
  )
}