from prometheus_client import Counter, Gauge


class MetricsRegistrar:
    COUNTERS = 'counters'
    GAUGES = 'gauges'

    def __init__(self):
        self.metrics_dict = {
            self.COUNTERS: {

            },
            self.GAUGES: {

            }
        }

    def counter(self, name, documentation=None):
        if name not in self.metrics_dict[self.COUNTERS]:
            if not documentation:
                documentation = name
            self.metrics_dict[self.COUNTERS][name] = Counter(name=name, documentation=documentation)

        return self.metrics_dict[self.COUNTERS][name]

    def gauge(self, name, documentation=None):
        if name not in self.metrics_dict[self.GAUGES]:
            if not documentation:
                documentation = name
            self.metrics_dict[self.GAUGES][name] = Gauge(name=name, documentation=documentation)

        return self.metrics_dict[self.GAUGES][name]
