#include <chrono>
#include <iostream>
#include <string>
#include <vector>

#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

#include <Eigen/Dense>

static Eigen::MatrixXd json_to_matrix(const nlohmann::json &a) {
  const int n = static_cast<int>(a.size());
  Eigen::MatrixXd A(n, n);
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      A(i, j) = a.at(i).at(j).get<double>();
    }
  }
  return A;
}

static Eigen::VectorXd json_to_vector(const nlohmann::json &b) {
  const int n = static_cast<int>(b.size());
  Eigen::VectorXd B(n);
  for (int i = 0; i < n; ++i) {
    B(i) = b.at(i).get<double>();
  }
  return B;
}

static nlohmann::json vector_to_json(const Eigen::VectorXd &x) {
  nlohmann::json j = nlohmann::json::array();
  for (int i = 0; i < x.size(); ++i)
    j.push_back(x(i));
  return j;
}

int main() {
  const std::string url = "http://127.0.0.1:8000";

  // --- GET task ---
  auto r_get = cpr::Get(cpr::Url{url});
  std::cout << "[GET] HTTP " << r_get.status_code << "\n";
  if (r_get.status_code != 200) {
    std::cerr << "GET failed:\n" << r_get.text << "\n";
    return 1;
  }

  nlohmann::json task = nlohmann::json::parse(r_get.text);

  // --- Parse A, b ---
  Eigen::MatrixXd A = json_to_matrix(task.at("a"));
  Eigen::VectorXd b = json_to_vector(task.at("b"));

  // --- Solve Ax=b and time it ---
  auto t0 = std::chrono::high_resolution_clock::now();
  Eigen::VectorXd x = A.colPivHouseholderQr().solve(b);
  auto t1 = std::chrono::high_resolution_clock::now();
  double elapsed =
      std::chrono::duration_cast<std::chrono::duration<double>>(t1 - t0)
          .count();

  // --- Update JSON ---
  task["x"] = vector_to_json(x);
  task["time"] = elapsed;

  // (Optionnel) petite vérif numérique
  double err = (A * x - b).norm();
  std::cout << "Solved. ||Ax-b|| = " << err << "  time=" << elapsed << "s\n";

  // --- POST result ---
  auto r_post = cpr::Post(cpr::Url{url},
                          cpr::Header{{"Content-Type", "application/json"}},
                          cpr::Body{task.dump()});

  std::cout << "[POST] HTTP " << r_post.status_code << "\n";
  std::cout << r_post.text << "\n";

  return (r_post.status_code == 200) ? 0 : 2;
}
