---
type: Source Summary
title: Elastic Distribution of OpenTelemetry for Node.js
source: https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/node/setup
description: Official setup, configuration, supported-instrumentation, and limitation guidance for Elastic's Node.js OpenTelemetry distribution.
tags: [elastic, observability, opentelemetry, edot, nodejs, instrumentation]
timestamp: 2026-09-08T10:10:59+01:00
---

# Summary

Elastic's EDOT Node.js package is `@elastic/opentelemetry-node`. The minimal documented setup installs the package, configures the OTLP endpoint, authorization header, and service name, then starts Node with `--import @elastic/opentelemetry-node` before the application's dependencies load.

EDOT automatically instruments supported Node.js modules and sends telemetry to the configured observability backend over OTLP. The supported-technologies page lists instrumentations and compatible versions, including Express, Knex, and `pg`. It also documents narrower ESM support. Unsupported components require a library's native OpenTelemetry support or manual instrumentation.

The configuration surface includes signal exporters, sampling, enabled or disabled instrumentations, host metrics, and logging-framework log sending. A tutorial should not imply that adding the package exposes every function call in arbitrary application code.

The setup guide warns against running EDOT Node.js alongside another APM agent in the same process because that can produce conflicting instrumentation or duplicate telemetry.

# Video guidance

- Show the package, required environment variables, and `--import` startup command as one coherent setup.
- Name the service explicitly so it does not appear as `unknown_service:node`.
- Describe the result as automatic instrumentation for supported modules, not complete access to application logic.
- State when manual spans or other instrumentation are needed.
- Verify that any framework versions used in the demo are supported, especially when the app uses ESM.

# Related official documentation

- [Configure the EDOT Node.js SDK](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/node/configuration)
- [Technologies supported by the EDOT Node.js SDK](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/node/supported-technologies)
