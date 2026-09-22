package com.sovereignnexus.smaos.guard;

import org.springframework.web.reactive.function.client.ClientRequest;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.ExchangeFilterFunction;
import org.springframework.web.reactive.function.client.ExchangeFunction;
import reactor.core.publisher.Mono;

/**
 * Enterprise Spring Boot / WebClient Remediation Filter (Moat 1 & DORA Art. 17)
 * Hard boundary invariant: Evidence Absent => UNKNOWN
 * Prevents Spring AI / LangChain4j harnesses from returning ungrounded confirmation.
 */
public class ProofOrStopFilter implements ExchangeFilterFunction {

    @Override
    public Mono<ClientResponse> filter(ClientRequest request, ExchangeFunction next) {
        return next.exchange(request)
            .onErrorResume(java.net.SocketTimeoutException.class, ex -> {
                // Hard boundary invariant: Evidence Absent => UNKNOWN
                return Mono.error(new AgentDiscrepancyException(
                    "DORA Art. 17 Violation: Wire dropped with no settlement receipt. State forced to UNKNOWN."
                ));
            });
    }
}
