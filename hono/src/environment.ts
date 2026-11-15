export function requiredEnvironment(name: string): string {
  const value = process.env[name]
  if (value === undefined || value.trim() === "") throw new Error(`Missing service configuration: ${name}`)
  return value
}
