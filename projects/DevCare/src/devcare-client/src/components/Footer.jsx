function Footer() {
  return (
    <footer className="border-t border-[var(--color-border)] bg-[rgba(255,255,255,0.72)] py-8">
      <div className="site-container flex flex-col gap-2 text-center sm:flex-row sm:items-center sm:justify-between sm:text-left">
        <p className="text-sm font-semibold text-[var(--color-text-muted)]">
          DevCare AI | Hackathon Project
        </p>
        <p className="text-sm text-[var(--color-text-muted)]">
          Designed for rapid prototyping in healthcare.
        </p>
      </div>
    </footer>
  )
}

export default Footer