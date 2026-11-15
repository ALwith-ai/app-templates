import { cleanup } from "@testing-library/react"
import { afterEach, beforeEach, expect } from "vitest"

beforeEach(() => {
  expect.hasAssertions()
})

afterEach(cleanup)
