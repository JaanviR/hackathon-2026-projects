const steps = [
  {
    title: 'Connect data streams',
    description:
      'Bring together EHR records, triage forms, and live monitoring feeds in one place.',
  },
  {
    title: 'Run AI analysis',
    description:
      'Apply your model to prioritize risk, detect anomalies, and suggest practical actions.',
  },
  {
    title: 'Support care decisions',
    description:
      'Present clear recommendations and alerts that clinicians can review quickly.',
  },
]

function HowItWorksSection() {
  return (
    <section id="how-it-works" className="site-container py-14 sm:py-16">
      <div className="rounded-3xl border border-[var(--color-border)] bg-[var(--color-surface-soft)] p-6 sm:p-10">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm font-bold uppercase tracking-[0.16em] text-[var(--color-primary)]">
            How It Works
          </p>
          <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
            Three simple steps for a strong hackathon demo
          </h2>
        </div>

        <div className="grid gap-5 md:grid-cols-3">
          {steps.map((step, index) => (
            <article
              key={step.title}
              className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
            >
              <p className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[var(--color-primary)] text-sm font-bold text-white">
                {index + 1}
              </p>
              <h3 className="mt-4 text-xl font-bold">{step.title}</h3>
              <p className="mt-2 text-sm leading-6 text-[var(--color-text-muted)] sm:text-base">
                {step.description}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}

export default HowItWorksSection