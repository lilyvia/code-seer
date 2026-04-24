package com.example.demo.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.http.ResponseEntity;
import javax.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("/api")
public class AuthDefectsController {

    // === VULNERABLE methods (should be detected) ===

    // Pattern 1: IDOR - Direct object return without ownership check
    @GetMapping("/orders/{id}")
    public Order getOrder(@PathVariable Long id) {
        return orderRepo.findById(id).orElseThrow();
    }

    // Pattern 2: Delete operation guarded only by isAuthenticated
    @PreAuthorize("isAuthenticated()")
    @DeleteMapping("/users/{id}")
    public void deleteUser(@PathVariable Long id) {
        userRepo.deleteById(id);
    }

    // Pattern 3: Sensitive write operation without any security annotation
    @DeleteMapping("/products/{id}")
    public void deleteProduct(@PathVariable Long id) {
        productRepo.deleteById(id);
    }

    @PutMapping("/products/{id}")
    public Product updateProduct(@PathVariable Long id, @RequestBody Product product) {
        return productRepo.save(product);
    }

    // Pattern 4: Direct findById return from request param
    @GetMapping("/users/lookup")
    public User lookupUser(HttpServletRequest request) {
        return userRepo.findById(request.getParameter("userId"));
    }

    // === SAFE methods (should NOT be detected) ===

    @PreAuthorize("hasRole('ADMIN')")
    @DeleteMapping("/admin/users/{id}")
    public void adminDeleteUser(@PathVariable Long id) {
        userRepo.deleteById(id);
    }

    @GetMapping("/orders/{id}/safe")
    public Order getOrderSafe(@PathVariable Long id, Authentication auth) {
        Order order = orderRepo.findById(id).orElseThrow();
        if (!order.getUserId().equals(auth.getName())) {
            throw new AccessDeniedException("Forbidden");
        }
        return order;
    }

    @PreAuthorize("hasAuthority('WRITE_PRODUCTS')")
    @PutMapping("/products/{id}/safe")
    public Product updateProductSafe(@PathVariable Long id, @RequestBody Product product) {
        return productRepo.save(product);
    }

    @GetMapping("/health")
    public String healthCheck() {
        return "ok";
    }
}

class FalseNegativeExpansionAuthJava {
    @PostMapping("/products")
    public Product false_negative_expansion_create(@RequestBody Product product) { return repo.save(product); }
    @PatchMapping("/products/{id}")
    public Product false_negative_expansion_patch(@PathVariable Long id, @RequestBody Product product) { return repo.save(product); }

    public void insecureSecurityConfig(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests().anyRequest().permitAll();
    }

    @GetMapping("/admin")
    public String adminDashboard() { return "admin"; }
}
