"""Atomic preflight patch for governed measurement transforms.

The measurement core validates transform authority per object. This wrapper adds
a batch-level preflight so a later constrained object cannot make a multi-object
quantize partially mutate earlier objects. It deliberately delegates the actual
metric quantization to measurement_system, preserving one implementation of the
unit contract.
"""


def install_atomic_quantize(measurement_system_module):
    original = measurement_system_module.quantize_world_location
    if getattr(original, "_oleander_atomic_batch", False):
        return original

    def atomic_quantize_world_location(scene, objects, step_mm, axes=(True, True, True)):
        batch = list(objects)
        for obj in batch:
            measurement_system_module._reject_transform_authority(obj)
        return original(scene, batch, step_mm, axes=axes)

    atomic_quantize_world_location._oleander_atomic_batch = True
    atomic_quantize_world_location.__name__ = "quantize_world_location"
    atomic_quantize_world_location.__doc__ = (
        "Quantize a complete object batch only after every object passes "
        "transform-authority preflight."
    )
    measurement_system_module.quantize_world_location = atomic_quantize_world_location
    return atomic_quantize_world_location
