%lang starknet

from starkware.cairo.common.math import assert_le

@external
func setup_examples() {
    %{
        max_examples(5)

        example(a=3, b=4)
        given(a = strategy.integers(10, 20), b = strategy.integers(30, 40))
        example(b=6, a=5)
    %}
    return ();
}

@external
func test_examples{syscall_ptr: felt*, range_check_ptr}(a: felt, b: felt) {
    assert_le(0, a);
    assert_le(0, b);
    assert_le(a, b);
    return ();
}

@external
func setup_examples_without_given() {
    %{
        example(a=3, b=4)
        example(b=6, a=5)
    %}
    return ();
}

@external
func test_examples_without_given{syscall_ptr: felt*, range_check_ptr}(a: felt, b: felt) {
    assert_le(0, a);
    assert_le(0, b);
    assert_le(a, b);
    return ();
}

@external
func setup_check_exact_example() {
    %{
        example(a=11, b=17)
    %}
    return ();
}

@external
func test_check_exact_example{syscall_ptr: felt*, range_check_ptr}(a: felt, b: felt) {
    %{
        assert ids.a == 11
        assert ids.b == 17
    %}
    return ();
}
