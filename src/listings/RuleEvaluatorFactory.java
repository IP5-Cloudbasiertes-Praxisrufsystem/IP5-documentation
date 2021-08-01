@Service
public class RuleEvaluatorFactory {

    private final Map<RuleType, RuleEvaluator> evaluators = new HashMap<>();

    @Autowired
    public RuleEvaluatorFactory(List<RuleEvaluator> evaluatorInstances) {
        evaluatorInstances.forEach(e -> evaluators.put(e.getRelevantType(), e));
    }

    public RuleEvaluator get(RuleType ruleType) {
        return evaluators.get(ruleType);
    }
}
