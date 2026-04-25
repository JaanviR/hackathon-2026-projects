const metrics = [
  { label: 'Faster triage estimates', value: '35%' },
  { label: 'Patient risk signal coverage', value: '24/7' },
  { label: 'Care team alert latency', value: '< 5m' },
]

function HeroSection() {
  return (
    <section id="home" className="site-container pb-14 pt-12 sm:pb-20 sm:pt-16">
      <div className="grid items-center gap-10 lg:grid-cols-[1.2fr_0.8fr]">
        <div>
          <p className="inline-flex rounded-full bg-[var(--color-surface-soft)] px-3 py-1 text-xs font-bold uppercase tracking-[0.16em] text-[var(--color-primary)]">
            AI in Healthcare
          </p>
          <h1 className="mt-4 text-4xl font-bold leading-tight sm:text-5xl lg:text-6xl">
            Smarter decisions for modern care teams.
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-[var(--color-text-muted)] sm:text-lg">
            DevCare AI helps clinicians and operations teams turn scattered
            healthcare data into quick, practical insights for better triage,
            monitoring, and follow-up.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <a href="#contact" className="btn-primary">
              Get started
            </a>
            <a href="#features" className="btn-secondary">
              See features
            </a>
          </div>
        </div>

        <aside className="elevated-card rounded-3xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 sm:p-7">
          <p className="text-sm font-bold uppercase tracking-[0.16em] text-[var(--color-primary)]">
            Snapshot
          </p>
          <h2 className="mt-3 text-2xl font-bold">Pilot performance metrics</h2>

          <div className="mt-6 space-y-4">
            {metrics.map((metric) => (
              <div
                key={metric.label}
                className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface-soft)] px-4 py-3"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.1em] text-[var(--color-text-muted)]">
                  {metric.label}
                </p>
                <p className="mt-1 text-2xl font-extrabold text-[var(--color-primary-strong)]">
                  {metric.value}
                </p>
              </div>
            ))}
          </div>
        </aside>
      </div>
    </section>
  )
}

export default HeroSection