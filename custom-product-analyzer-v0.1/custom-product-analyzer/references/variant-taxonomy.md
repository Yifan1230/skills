# Variant Taxonomy

## 变体类型

### standard-name
与标品同名。

不代表一定定制，必须进一步比较。

### $A-extension
形如：

```text
xkglapp$A
```

优先解释为对 canonical app 的扩展/覆盖型变体。

### school-suffix-copy
形如：

```text
xkglappbit
xkglappbuaa
xkglappfudan
```

identity 可能已替换，因此不能要求 identity 相同。

### r-directory-customization
位于：

```text
R\d+_XXX/
```

目录中的 canonical app 或其变体。

R 编号仅记录为 change_reference_id / context，不直接视作 Feature ID。

### identity-matched
应用名不同，但 app_info.xml identity 与标品一致。

### custom-independent
结构或业务强相关，但缺少可靠同源证据。

### uncertain
证据不足。

## 匹配证据

记录数组：

- exact_name
- dollar_a_pattern
- suffix_pattern
- r_directory
- identity_match
- path_similarity
- structure_similarity
- change_reference_match

## 剔除规则

名称含明显废弃标记：

- 已合并
- 勿用
- backup
- bak
- old
- deprecated

默认剔除或标低置信度。
