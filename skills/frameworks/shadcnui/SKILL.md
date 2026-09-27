---
name: shadcnui
description: Expert shadcn/ui assistance covering Radix UI primitives, Tailwind CSS styling, copy-paste architecture, and accessibility. Use when building modern React component systems and accessible design systems.
---

# shadcn/ui

shadcn/ui is not a component library; it's a **collection of reusable components** that you copy and paste into your apps. Built on Radix UI and Tailwind.

## When to Use

- **Modern Copy-Paste Component Architecture**: Full ownership of React UI components without npm dependency lock-in.
- **Accessible Design Systems with Tailwind CSS & Radix UI**: Fully accessible WAI-ARIA primitives styled with Tailwind.
- **Next.js & Vite Modern Web Applications**: Building polished SaaS dashboards and web interfaces.
- **Themable Component Libraries**: Customizing CSS variables, radius, and neutral color palettes.

## Quick Start

```bash
# Initialize shadcn in your Next.js / Vite project
npx shadcn@latest init

# Add components
npx shadcn@latest add button card dialog
```

```tsx
import { Button } from "@/components/ui/button";

export default function Demo() {
  return (
    <Button variant="outline" size="lg">
      shadcn Button
    </Button>
  );
}
```

## Core Concepts

#Composable Dialog Primitive with Radix UI

Accessible modal dialogs adhering to open standards:

```tsx
import * as React from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

export function ConfirmActionModal() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete Account</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Are you absolutely sure?</DialogTitle>
          <DialogDescription>
            This action cannot be undone. This will permanently delete your
            account and remove your data.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline">Cancel</Button>
          <Button variant="destructive">Confirm Deletion</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

#Type-Safe Forms with React Hook Form & Zod

Form validation with accessible field bindings:

```tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const formSchema = z.object({
  email: z.string().email("Invalid email format"),
});

export function SubscribeForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "" },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log("Submitted:", values);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email Address</FormLabel>
              <FormControl>
                <Input placeholder="you@domain.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Subscribe</Button>
      </form>
    </Form>
  );
}
```

#Component Styling with cn() & class-variance-authority (cva)

Customizing variants with merge utility:

```tsx
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/80",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/80",
        outline: "text-foreground border border-input",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

export function Badge({
  className,
  variant,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof badgeVariants>) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}
```

## Common Patterns

### Composed Dialog with Form Validation

**Problem**: Creating modal forms with focus trap, backdrop dismissal, and accessible keyboard navigation.

**Solution**:
Compose Radix Dialog with Tailwind classes:

```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

export function ConfirmModal() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete Item</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Are you absolutely sure?</DialogTitle>
          <DialogDescription>
            This action cannot be undone. This will permanently delete your
            account.
          </DialogDescription>
        </DialogHeader>
        <div className="flex justify-end gap-3 mt-4">
          <Button variant="outline">Cancel</Button>
          <Button variant="destructive">Confirm Delete</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

## Best Practices (2026)

- **Do** install components on demand using the CLI (`npx shadcn@latest add button`) rather than copying everything at once.
- **Do** use the `cn()` utility (`clsx` + `tailwind-merge`) to safely merge custom class names with defaults.
- **Do** use `asChild` prop on triggers to avoid rendering invalid nested interactive HTML elements (e.g. button inside button).
- **Do** define theme tokens in `globals.css` with HSL / OKLCH CSS variables for easy dark mode adaptation.
- **Don't** treat `@/components/ui` as an external third-party library; feel free to modify components directly.
- **Don't** bypass Radix accessibility primitives for complex interactive components like dropdowns and dialogs.
- **Don't** remove ARIA attributes or focus styling from components.

## Troubleshooting

| Error                                         | Cause                                                | Solution                                                                                  |
| :-------------------------------------------- | :--------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| `Cannot find module '@/components/ui/button'` | Path alias `@/*` not configured in `tsconfig.json`.  | Add `"paths": { "@/*": ["./src/*"] }` to `compilerOptions` in tsconfig.                   |
| `Styles missing / components appear unstyled` | Tailwind CSS not scanning component directory.       | Add `"./src/components/**/*.{js,ts,jsx,tsx}"` to `content` array in `tailwind.config.js`. |
| `Tailwind merge error: clsx is not defined`   | Missing `clsx` or `tailwind-merge` utility packages. | Run `npm install clsx tailwind-merge`.                                                    |

## References

- [shadcn/ui Documentation](https://ui.shadcn.com/)
