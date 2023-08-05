@classmethod
    def _sample_log_prob(cls, dist, sample):
        tensor = dist.log_prob(tf.stop_gradient(sample.tensor))
        scope = []
        batch = sample.batch
        return TensorFluent(tensor, scope, batch)

    @classmethod
    def _deterministic_log_prob(cls, fluent):
        tensor = tf.constant(0.0, shape=fluent.shape._shape)
        scope = []
        batch = fluent.batch
        return TensorFluent(tensor, scope, batch)

    @classmethod
    def _sum_log_probs(cls, *args):
        total_log_prob = None
        for arg in args:
            if arg is not None:
                if total_log_prob is None:
                    total_log_prob = arg
                else:
                    total_log_prob += arg
        return total_log_prob

    @classmethod
    def _condition_log_prob(cls, condition, true_case, false_case, condition_log_prob, true_case_log_prob, false_case_log_prob):
        if condition_log_prob is None and true_case_log_prob is None and false_case_log_prob is None:
            return None

        true_total_log_prob = cls._sum_log_probs(condition_log_prob, true_case_log_prob)
        if true_total_log_prob is None:
            true_total_log_prob = cls._deterministic_log_prob(true_case)

        false_total_log_prob = cls._sum_log_probs(condition_log_prob, false_case_log_prob)
        if false_total_log_prob is None:
            false_total_log_prob = cls._deterministic_log_prob(false_case)

        true = TensorFluent.constant(True, tf.bool)
        false = TensorFluent.constant(False, tf.bool)
        log_prob_fluent = (condition == true) * true_total_log_prob + (condition == false) * false_total_log_prob
        tensor = log_prob_fluent.tensor
        scope = []
        batch = condition.batch
        return TensorFluent(tensor, scope, batch)

    @classmethod
    def _aggregation_log_prob(cls, log_prob, fluent, vars_list):
        if log_prob is None:
            return None
        axis = TensorFluent._varslist2axis(fluent, vars_list)
        tensor = tf.reduce_sum(log_prob.tensor, axis=axis)
        scope = []
        batch = fluent.batch
        return TensorFluent(tensor, scope, batch)
