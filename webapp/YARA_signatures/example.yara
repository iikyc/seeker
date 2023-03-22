rule test_rule {
    strings:
        $a = "find"
    condition:
        $a
}

rule test_rule_2 {
    meta:
        author = "Karam"
        description = "Test YARA Rule"
    strings:
        $a = "sudo"
    condition:
        $a
}